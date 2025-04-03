package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.Duration;
import java.time.LocalDate;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.PouleRepository;
import com.example.tinyfarm.repository.ProduitRepository;
import com.example.tinyfarm.repository.RemiseRepository;

import org.springframework.data.domain.Page;
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
        long differenceInDays = Duration.between(poule.getDernierRepas(), LocalDateTime.now()).toDays();
        
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
        
        if (Duration.between(poule.getMaladeDepuis(), LocalDateTime.now()).toDays() >= 4) {
            pouleRepository.deleteById(id); // La poule meurt, on la supprime
        }
    
    }

    @Transactional
    public Poule nourrirPoule(Long id, String nourriture) {
        Optional<Poule> optPoule = pouleRepository.findById(id);
        if (!optPoule.isPresent()) {
            return null;
        }
        
        Poule poule = optPoule.get();
        if (poule.getDernierRepas() != null && poule.getDernierRepas().isBefore(LocalDateTime.now().minusHours(24)) && poule.getProprietaire().getEcus()>=3) {
            if (nourriture.equals("Grain")) {
                Optional<Produit> existp = produitRepository.findByNom("Grain");
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
                    if (poule.getPoids()+0.5 <= 3.5){
                        poule.setPoids(poule.getPoids() + 0.5);
                    }
                    else if (poule.getPoids()<3.5 && poule.getPoids()+0.5 > 3.5 ){
                        poule.setPoids(3.5);
                    }
                    poule.setDernierRepas(LocalDateTime.now());
                    remise.setQuantite(remise.getQuantite()-1);
                    remiseRepository.save(remise);
                }
            }

            poule.getProprietaire().setEcus(poule.getProprietaire().getEcus()-3);
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
}