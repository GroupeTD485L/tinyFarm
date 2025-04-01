
package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.Optional;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import  com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.entity.Remise;
import  com.example.tinyfarm.entity.Commerce;
import  com.example.tinyfarm.entity.Produit;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.service.CommerceService;
import  com.example.tinyfarm.entity.Compte;
import  com.example.tinyfarm.service.CompteService;
import  com.example.tinyfarm.service.RemiseService;
import  com.example.tinyfarm.service.ProduitService;
import  com.example.tinyfarm.repository.RemiseRepository;




@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{idFerme}/remise")
public class RemiseController {
    
    private final RemiseService remiseService;
    private final FermeService fermeService;
    private final CompteService compteService;
    private final ProduitService produitService;
    private final RemiseRepository remiseRepository;

    public RemiseController(CompteService compteService, FermeService fermeService, RemiseService remiseService, ProduitService produitService, RemiseRepository remiseRepository) {
        this.remiseService = remiseService;
        this.fermeService = fermeService;
        this.compteService = compteService;
        this.produitService = produitService;
        this.remiseRepository = remiseRepository;

    }

    @PostMapping
    public ResponseEntity<Remise> rajouterProduit(@PathVariable Long fermeId, @RequestBody String nomProduit) {
        Ferme ferme = fermeService.getFerme(fermeId);
        Produit produit = produitService.getProduit(nomProduit);
        Remise remise = remiseService.addProduit2Remise(ferme, produit);

        if(produit == null || remise == null)
            return ResponseEntity.notFound().build();

        return ResponseEntity.ok(remise);
    }


    @PreAuthorize("isAuthenticated()")
    @GetMapping
    public ResponseEntity<List<Remise>> infoRemise(@PathVariable Long fermeId) {
        Ferme ferme = fermeService.getFerme(fermeId);
        List<Remise> remises = remiseService.getInfoRemise(ferme);

        for (Remise remise : remises) {
            if (remise == null)
                return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(remises);
    }
    
    //IDK how to w/ getInfoProduit in service
    @GetMapping("/{idProduit}")
    public ResponseEntity<Remise> infoProduit(@PathVariable Long fermeId, @RequestBody String nomProduit){
        Ferme ferme = fermeService.getFerme(fermeId);
        Produit produit = produitService.getProduit(nomProduit);
        Optional<Remise> optionalRemise = remiseRepository.findByIdProduitAndProprietaire(produit,ferme);

        if (optionalRemise == null)
            return ResponseEntity.notFound().build();
            
        Remise remise = optionalRemise.get();

        return ResponseEntity.ok(remise);
    }
    

    @PutMapping("/{id}")
    public ResponseEntity<Remise> updateProduit(@PathVariable Long fermeId, @RequestBody String nomProduit, @RequestParam int quantite) {
        Ferme ferme = fermeService.getFerme(fermeId);
        Produit produit = produitService.getProduit(nomProduit);
        Remise updatedRemise = remiseService.updateRemiseProduit(ferme, produit, quantite);

        if (updatedRemise == null)
            return ResponseEntity.notFound().build();

        return ResponseEntity.ok(updatedRemise);
    }

    
    @DeleteMapping
    public ResponseEntity<List<Remise>> deleteRemise(@PathVariable Long fermeId) {
        List<Remise> deletedRemises = remiseService.deleteRemises(fermeService.getFerme(fermeId));

        return ResponseEntity.ok(deletedRemises);
    }

}
 