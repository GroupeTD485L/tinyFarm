package com.example.tinyfarm.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.entity.Produit;
import com.example.tinyfarm.entity.Remise;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.RemiseRepository;



@Service
public class RemiseService {

    private final RemiseRepository remiseRepository;
    private final FermeRepository fermeRepository;
    
    public RemiseService( RemiseRepository remiseRepository, FermeRepository fermeRepository) {
        this.remiseRepository = remiseRepository;
        this.fermeRepository = fermeRepository;
    }

    @Transactional 
    public Remise createRemise (Ferme ferme, Produit produit){
       Remise r = new Remise();
       r.setIdProduit(produit);
        r.setQuantite(1);
        r.setProprietaire(ferme);
        return remiseRepository.save(r);
    }

    @Transactional 
    public Remise addProduit2Remise (Ferme ferme, Produit produit){
       Optional<Remise> remise = remiseRepository.findByProprietaireAndIdProduit(ferme,produit);
        if (!remise.isPresent()){
            return remiseRepository.save (createRemise(ferme, produit));
        }
        else {
        Remise r = remise.get();
        r.setQuantite(r.getQuantite()+1);
        return remiseRepository.save(r);
        }
    }

    @Transactional 
    public List<Remise> getInfoRemise (Ferme ferme){
       return remiseRepository.findByProprietaire(ferme);
        
    }

    @Transactional 
    public Remise updateRemiseProduit (Ferme ferme,Produit produit,int quantiteAMettre){
        Optional<Remise> r = remiseRepository.findByProprietaireAndIdProduit(ferme,produit);
        if (!r.isPresent()){
            return null;
        }
        Remise remise = r.get();
        remise.setQuantite(quantiteAMettre);
        return remiseRepository.save(remise);

    }

    @Transactional 
    public List<Remise> deleteRemises (Ferme ferme){
       List<Remise> r = remiseRepository.findByProprietaire(ferme);
        for (Remise remise : r){
            remiseRepository.delete(remise);
        }
        ferme.setRemise(null);
            fermeRepository.save(ferme);
        return r;
    }

    
}
/*
5 - Gestion de la remise
POST      /comptes/{id}/fermes/{id}/remise  Rajoute un produit à la remise
GET         /comptes/{id}/fermes/{id}/remise Obtenir tout ce qu'il y as dans la remise
GET         /comptes/{id}/fermes/{id}/remise/{id}  Obtenir les données d'un des produits
PUT         /comptes/{id}/fermes/{id}/remise/{id}  Update les données d'un des produits
DELETE /comptes/{id}/fermes/{id}/remise  Detruire la remise
 */