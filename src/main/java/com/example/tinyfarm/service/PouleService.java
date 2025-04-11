package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.Duration;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.PouleRepository;
import com.example.tinyfarm.repository.ProduitRepository;
import com.example.tinyfarm.repository.RemiseRepository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.util.Optional;
import java.util.Random;

@Service
public class PouleService {

    private final PouleRepository pouleRepository;
    private final FermeRepository fermeRepository;
    private final RemiseRepository remiseRepository;
    private final ProduitRepository produitRepository;

    public PouleService(PouleRepository pouleRepository, FermeRepository fermeRepository, RemiseRepository remiseRepository,ProduitRepository produitRepository) {
        this.pouleRepository = pouleRepository;
        this.fermeRepository = fermeRepository;
        this.remiseRepository = remiseRepository;
        this.produitRepository = produitRepository;
    }

    @Transactional
    public Page<Poule> getAllPoules(Pageable pageable) {
        return pouleRepository.findAll(pageable);
    }

    @Transactional
    public Page<Poule> getAllMyPoules(Ferme ferme, Pageable pageable) {
        return pouleRepository.findAllByProprietaire(ferme, pageable);
    }

    @Transactional
    public Page<Poule> getPoulesByProprietaireAndSexe(Ferme ferme, char sexe, Pageable pageable) {
        return pouleRepository.findAllByProprietaireAndSexe(ferme, sexe, pageable);
    }

    @Transactional
    public Page<Poule> getPoulesBySexe(char sexe, Pageable pageable) {
        return pouleRepository.findAllBySexe(sexe, pageable);
    }

    @Transactional
    public Optional<Poule> getPouleById(Long id) {
        return pouleRepository.findById(id);
    }

    @Transactional
    public Poule addPoule(Poule poule) {
        return pouleRepository.save(poule);
    }

    @Transactional
    public void deletePoule(Long id) {
        pouleRepository.deleteById(id);
    }

    @Transactional
    public void updatePoule(Long id) {
        Optional<Poule> existingPoule = pouleRepository.findById(id);
        Poule poule = existingPoule.get();
        long differenceInDays = poule.getDernierRepas() != null 
        ? Duration.between(poule.getDernierRepas(), LocalDateTime.now()).toDays() : Long.MAX_VALUE;
        poule.setAge(poule.getAge()+1);
        if ( differenceInDays == 1) {
            poule.setPoids(poule.getPoids()-0.2);
        } else if ( differenceInDays == 2) {
            poule.setPoids(poule.getPoids()-0.5);
        } else if ( differenceInDays == 3) {
            poule.setPoids(poule.getPoids()-1);
        } else if (differenceInDays >= 4) {
            pouleRepository.deleteById(id); // La poule meurt, on la supprime
        }
        if (poule.getAge()==5 && poule.getPoids()>= 2.5) {
            Random random = new Random();
            poule.setSexe(random.nextBoolean() ? 'M' : 'F');
        }
        if (poule.getMaladeDepuis() != null) {
            if (Duration.between(poule.getMaladeDepuis(), LocalDateTime.now()).toDays() >= 4)  {
                pouleRepository.deleteById(id); // La poule meurt, on la supprime
            }
        }
        
    
    }

    @Transactional
    public void updateAllPoules(){
        int iPage = 0;
        Page<Poule> poules;
        do {
            poules = pouleRepository.findAll(PageRequest.of(iPage, 20));
            for (Poule poule : poules) {
                Long id = poule.getIdPoule();
                updatePoule(id);
            }
            iPage++;
        } while (poules.hasNext());
    }

    @Transactional
    public Poule nourrirPoule(Long id, String nourriture) {
        Optional<Poule> optPoule = pouleRepository.findById(id);
        if (!optPoule.isPresent()) {
            System.out.println("Poule non trouvée avec l'ID : " + id);
            return null;
        }

        Poule poule = optPoule.get();
        System.out.println("Dernier repas : " + poule.getDernierRepas());
        System.out.println("Poids actuel : " + poule.getPoids());
        System.out.println("Ecus du propriétaire : " + poule.getProprietaire().getEcus());

        if (poule.getDernierRepas() == null) {
            System.out.println("Dernier repas est null - la poule n'a jamais été nourrie");
        } else if (!poule.getDernierRepas().isBefore(LocalDateTime.now().minusHours(24))) {
            System.out.println("La poule a déjà été nourrie dans les dernières 24 heures");
            return poule;
        } else if (poule.getProprietaire().getEcus() < 3) {
            System.out.println("Le propriétaire n'a pas assez d'écus");
            return poule;
        }
        if (poule.getDernierRepas() != null 
        && poule.getDernierRepas().isBefore(LocalDateTime.now().minusHours(24)) && poule.getProprietaire().getEcus() >= 3) {
            if (nourriture.equals("Graine")) {
                Optional<Produit> existp = produitRepository.findByNom("Graine");
                if (!existp.isPresent()) {
                    throw new IllegalArgumentException("Le produit n'existe pas");
                }

                Produit p = existp.get();
                Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p, poule.getProprietaire());
                if (!existingRemise.isPresent()) {
                    throw new IllegalArgumentException("Produit non trouvé dans la remise");
                }

                Remise remise = existingRemise.get();
                System.out.println("Quantité dans la remise : " + remise.getQuantite());
                if (remise.getQuantite() > 0) {
                    if (poule.getPoids() + 0.5 <= 3.5) {
                        poule.setPoids(poule.getPoids() + 0.5);
                    } else if (poule.getPoids() < 3.5 && poule.getPoids() + 0.5 > 3.5) {
                        poule.setPoids(3.5);
                    }
                    poule.setDernierRepas(LocalDateTime.now());
                    remise.setQuantite(remise.getQuantite() - 1);
                    remiseRepository.save(remise);
                }
            }

            poule.getProprietaire().setEcus(poule.getProprietaire().getEcus() - 3);
            return pouleRepository.save(poule);
        }
        return poule;
    }

    @Transactional
    public Poule abreuverPoule(Long id, String nourriture) {
        Optional<Poule> optPoule = pouleRepository.findById(id);
        if (!optPoule.isPresent()) {
            return null;
        }
        
        Poule poule = optPoule.get();
        if (poule.getDernierBreuvage() != null && poule.getDernierBreuvage().isBefore(LocalDateTime.now().minusHours(24)) && poule.getProprietaire().getEcus()>=1) {
            if (nourriture.equals("Seau d'eau")) {
                Optional<Produit> existp = produitRepository.findByNom("Seau d'eau");
                if (!existp.isPresent()) {
                    throw new IllegalArgumentException("Le produit n'existe pas");
                }
                Produit p = existp.get();
                Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,poule.getProprietaire());
                if (!existingRemise.isPresent()) {
                    throw new IllegalArgumentException("Produit non trouvé dans la remise");
                }
                Remise remise = existingRemise.get();

                if ( remise.getQuantite() > 0 ){
                    if (poule.getDernierRepas()==LocalDateTime.now().minusHours(24)) {
                        if (poule.getPoids()+0.5 <= 3.5){
                            poule.setPoids(poule.getPoids() + 0.5);
                        }
                        else if (poule.getPoids()<3.5 && poule.getPoids()+0.5 > 3.5 ){
                            poule.setPoids(3.5);
                        }
                    }
                    poule.setDernierBreuvage(LocalDateTime.now());
                    remise.setQuantite(remise.getQuantite()-1);
                    remiseRepository.save(remise);
                }
            }
            poule.getProprietaire().setEcus(poule.getProprietaire().getEcus()-1);
            return pouleRepository.save(poule);
        }
        return poule;
    }

    @Transactional
    public Poule laverPoule(Long id) {
        Optional<Poule> optPoule = pouleRepository.findById(id);
        if (!optPoule.isPresent()) {
            return null;
        }
        
        Poule poule = optPoule.get();

        Optional<Produit> existp =  produitRepository.findByNom("Savon");
        if (!existp.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit p = existp.get();

        Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,poule.getProprietaire());
        if (!existingRemise.isPresent()) {
            throw new IllegalArgumentException("Produit non trouvé dans la remise");
        }
        Remise remise = existingRemise.get();
        if (remise.getQuantite()>0 ){
            remise.setQuantite(remise.getQuantite()-1);
            poule.setDernierLavage(LocalDateTime.now());
        }
                
        return pouleRepository.save(poule);
    }

    @Transactional
    public Poule soignerPoule(Long id) {
        Optional<Poule> optPoule = pouleRepository.findById(id);
        if (!optPoule.isPresent()) {
            return null;
        }
        
        Poule poule = optPoule.get();
        
        // Si la vache est malade, on la soigne
        if (poule.getMaladeDepuis() != null) {
            Optional<Produit> existp =  produitRepository.findByNom("Seringue");
            if (!existp.isPresent()) {
                throw new IllegalArgumentException("Le produit n'existe pas");
            }
            Produit p = existp.get();
            
            Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,poule.getProprietaire());
            if (!existingRemise.isPresent()) {
                throw new IllegalArgumentException("Produit non trouvé dans la remise");
            }
            Remise remise = existingRemise.get();
            if (remise.getQuantite()>0 ){
                remise.setQuantite(remise.getQuantite()-1);
                poule.setMaladeDepuis(null);
            }
            
            return pouleRepository.save(poule);
        }

        return(poule);
    }
    // Ajout d'une méthode pour rendre une poule malade
    @Transactional
    public Poule rendreMaladePoule(Long id, Ferme ferme) {
        Optional<Poule> optPoule = pouleRepository.findById(id);
        if (!optPoule.isPresent()) {
            return null;
        }
    
        Poule poule = optPoule.get();
        // Ignorer le paramètre ferme car non nécessaire pour cette fonctionnalité
        poule.setMaladeDepuis(LocalDateTime.now().minusDays(2));
        return pouleRepository.save(poule);
    }
}

    
