package com.example.tinyfarm.service;

import java.time.LocalDateTime;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.Clapier;
import com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.entity.Produit;
import com.example.tinyfarm.entity.Remise;
import com.example.tinyfarm.repository.ClapierRepository;
import com.example.tinyfarm.repository.RemiseRepository;
import com.example.tinyfarm.repository.ProduitRepository;

@Service
public class ClapierService {
    private final ClapierRepository clapierRepository;
    private final RemiseRepository remiseRepository;
    private final ProduitRepository produitRepository;
    private final FermeService fermeService;

    public ClapierService(ClapierRepository clapierRepository, RemiseRepository remiseRepository,ProduitRepository produitRepository,FermeService fermeService) {
        this.clapierRepository = clapierRepository;
        this.remiseRepository = remiseRepository;
        this.produitRepository = produitRepository;
        this.fermeService = fermeService;
    }
    @Transactional
    public Clapier creerClapier(String pseudo) {
        return null;
    }
    @Transactional
    public Clapier getInfoClapier(String pseudo) {
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);
        long fermeId = ferme.getIdFerme();
        Optional<Clapier> clapier = clapierRepository.findById(fermeId);
        if (clapier.isPresent()) {
            return clapier.get();
        } else {
            return null;
        }
    }

    @Transactional
    public Clapier updateClapier(String pseudo) {
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);
        Clapier clapier = ferme.getClapier();
        if (clapier == null) {
            return null;
        }

        if (clapier.getDernierRepas().isAfter(LocalDateTime.now().minusDays(1)) 
            && clapier.getDernierBreuvage().isAfter(LocalDateTime.now().minusDays(1)) ){
                if (clapier.getNb_gros() %2 == 0 ){
                clapier.setNb_adulte_m(clapier.getNb_adulte_m() + clapier.getNb_gros()/2);
                clapier.setNb_adulte_f(clapier.getNb_adulte_f() + clapier.getNb_gros()/2);
                }
                else {
                    clapier.setNb_adulte_m(clapier.getNb_adulte_m() + clapier.getNb_gros()/2);
                    clapier.setNb_adulte_f(clapier.getNb_adulte_f() + clapier.getNb_gros()/2 +1);
                }
                clapier.setNb_gros(clapier.getNb_petit());
                clapier.setNb_petit(clapier.getNb_bebe());
                clapier.setNb_bebe(0);
                

        }
        if (clapier.getDernierRepas().isBefore(LocalDateTime.now().minusDays(1))){
            if(clapier.getNb_bebe()!=0){
                clapier.setNb_bebe(0);
            }else if(clapier.getNb_petit()!=0){
                clapier.setNb_petit(0);
            }else if(clapier.getNb_gros()!=0){
                clapier.setNb_gros(0);
            }
            
            if(clapier.getNb_adulte_f()!=0){
                clapier.setNb_adulte_f(clapier.getNb_adulte_f()-clapier.getNb_adulte_f()/3);
            }else if(clapier.getNb_adulte_m()!=0){
                clapier.setNb_adulte_m(clapier.getNb_adulte_m()-clapier.getNb_adulte_m()/3);
            }
        }
        

        

        return clapierRepository.save(clapier);
    }

    @Transactional
    public Clapier nourrirClapier(String pseudo) {
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);
        Clapier clapier = ferme.getClapier();
        if (clapier == null) {
            return null;
        }
        
        
        if (clapier.getDernierRepas() != null && 
        clapier.getDernierRepas().isBefore(LocalDateTime.now().minusHours(24))) {
            Optional<Produit> existp =  produitRepository.findByNom("Graine");
            if (!existp.isPresent()) {
                throw new IllegalArgumentException("Le produit n'existe pas");
            }
            Produit p = existp.get();    
            Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,clapier.getProprietaire());
            if (!existingRemise.isPresent()) {
                throw new IllegalArgumentException("Produit non trouvé dans la remise");
            }
            Remise remise = existingRemise.get();
            if (remise.getQuantite()>0 ){
                clapier.setDernierRepas(LocalDateTime.now());
                remise.setQuantite(remise.getQuantite()-1);
            }
        }
        return clapierRepository.save(clapier);
    }

    @Transactional
    public Clapier abbreuverClapier(String pseudo) {
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);
        Clapier clapier = ferme.getClapier();
        
        if (clapier == null) {
            return null;
        }

        Optional<Produit> existp =  produitRepository.findByNom("Seau d'eau");
        if (!existp.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit p = existp.get();
        
        Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,clapier.getProprietaire());
        if (!existingRemise.isPresent()) {
            throw new IllegalArgumentException("Produit non trouvé dans la remise");
        }
        Remise remise = existingRemise.get();
        if (remise.getQuantite()>0 ){
            clapier.setDernierBreuvage(LocalDateTime.now());
            remise.setQuantite(remise.getQuantite()-1);
        }

        return clapierRepository.save(clapier);
    }

    @Transactional
    public Clapier SoignerClapier(String pseudo) {
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);
        Clapier clapier = ferme.getClapier();
        if (clapier == null) {
            return null;
        }

        Optional<Produit> existp =  produitRepository.findByNom("Seringue");
        if (!existp.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit p = existp.get();
        Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,clapier.getProprietaire());
        if (!existingRemise.isPresent()) {
            throw new IllegalArgumentException("Produit non trouvé dans la remise");
        }
        Remise remise = existingRemise.get();
        if (remise.getQuantite()>0 ){
            clapier.setMaladeDepuis(null);
            remise.setQuantite(remise.getQuantite()-1);
        }
            
        return clapierRepository.save(clapier);
    }

    @Transactional
    public Clapier laverClapier(String pseudo) {
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);
        Clapier clapier = ferme.getClapier();
        if (clapier == null) {
            return null;
        }

        Optional<Produit> existp =  produitRepository.findByNom("Savon");
        if (!existp.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit p = existp.get();
            
        Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,clapier.getProprietaire());
        if (!existingRemise.isPresent()) {
            throw new IllegalArgumentException("Produit non trouvé dans la remise");
        }
        Remise remise = existingRemise.get();
        if (remise.getQuantite()>0 ){
            clapier.setDernierLavage(LocalDateTime.now());
            remise.setQuantite(remise.getQuantite()-1);
        }
                
        return clapierRepository.save(clapier);
    }

    @Transactional
    public void supprimerClapier(String pseudo) {
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);
        long fermeId = ferme.getIdFerme();
        clapierRepository.deleteById(fermeId);
    }
}


/*
POST      /comptes/{id}/fermes/{id}/clapier  Créer le clapier
GET         /comptes/{id}/fermes/{id}/clapier Obtenir les infos du clapier

PUT         /comptes/{id}/fermes/{id}/clapier Update les infos du clapier
PUT         /clapier/nourrir Nourrit les membres du clapier
PUT         /clapier/abreuver Abreuver les membres du clapier
PUT         /clapier/soigner Soigner les membres du clapier
PUT         /clapier/laver Laver les membres du clapier
*/