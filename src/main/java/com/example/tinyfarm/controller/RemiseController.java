/*
package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;

import java.util.Optional;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.entity.Remise;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Commerce;
import  com.example.tinyfarm.service.CommerceService;
import  com.example.tinyfarm.entity.Compte;
import  com.example.tinyfarm.service.CompteService;

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{id}/fermes/{id}/remise")
public class RemiseController {
    
    private final RemiseService remiseService;
    private final FermeService fermeService;
    private final CompteService compteService;

    public CommerceController(CompteService compteService, FermeService fermeService, RemiseService remiseService){
        this.remiseService = remiseService;
        this.fermeService = fermeService;
        this.compteService = compteService;
    }

    @PostMapping
    public ResponseEntity<Remise> rajouterProduit(@PathVariable Long fermeId, @RequestParam Long produitId) {
        Ferme ferme = fermeService.getFermeById(fermeId);
        Produit produit = produitService.getProduitById(produitId);

        if(produit == null)
            return ResponseEntity.notFound().build();

        Remise remise = remiseService.addProduit2Remise(ferme, produit);

        if (remise == null || remise.isEmpty()) 
            remise = remiseService.createRemise(ferme, produit);
        
        return ResponseEntity.ok(remise);
    }


    @PreAuthorize("isAuthenticated()")
    @GetMapping
    public Remise infoRemise(@PathVariable Long fermeId) {
        Ferme ferme = fermeService.getFermeById(fermeId);
        List<Remise> remises = remiseService.getInfoRemise(ferme);

        return ResponseEntity.ok(remises);
    }
    
    //IDK how to w/ getInfoProduit in service
    @GetMapping("/{id}")
    public Produit infoProduit(@PathVariable Long fermeId, @PathVariable Long nomProduit){
        Ferme ferme = fermeService.getFermeById(fermeId);
        Produit produit = produitService.getProduit(nomProduit);
        Optional<Remise> remise = remiseRepository.findByProprietaireAndIdProduit(ferme, produit);

        if (remise == null || remise.isEmpty())
            return ResponseEntity.notFound().build();

        return ResponseEntity.ok(remise.get());
    }
    

    @PutMapping("/{id}")
    public void updateProduit(@PathVariable Long fermeId, @PathVariable Long produitId, @RequestParam int quantite) {
        Ferme ferme = fermeService.getFermeById(fermeId);
        Produit produit = produitService.getProduitById(produitId);
        Remise updatedRemise = remiseService.updateRemiseProduit(ferme, produit, quantite);

        if (!updatedRemise.isPresent())
            return ResponseEntity.notFound().build();

        return ResponseEntity.ok(updatedRemise);
    }

    
    @DeleteMapping
    public void deleteRemise(@PathVariable Long fermeId) {
        List<Remise> deletedRemises = remiseService.deleteRemises(ferme);

        return ResponseEntity.ok(deletedRemises);
    }

}

 */

 