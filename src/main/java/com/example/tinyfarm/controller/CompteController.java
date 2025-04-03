package com.example.tinyfarm.controller;

import java.net.Authenticator;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import  com.example.tinyfarm.entity.Compte;
import  com.example.tinyfarm.service.CompteService;

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/comptes/") // URL
public class CompteController {
    
    private final CompteService compteService;

    public CompteController(CompteService compteService){
        this.compteService = compteService;
    }


    // Obtenir les infos du compte
    @PreAuthorize("isAuthenticated()")
    @GetMapping
    public ResponseEntity<Compte> infoCompte(Authentication authentication){
        // Récupérer le nom d'utilisateur de l'authentification (car la méthode getCompte prend un String)
        String pseudo = authentication.getName();
        // On get le compte
        Compte compte = compteService.getCompte(pseudo);

        return ResponseEntity.ok(compte); // On renvoie le compte existante
    }


    // Mettre à jour le compte
    @PreAuthorize("isAuthenticated()")
    @PutMapping
    public ResponseEntity<Compte> updateCompte(Authentication authentication){
        // Récupérer le nom d'utilisateur de l'authentification (car la méthode updateCompte prend un String)
        String pseudo = authentication.getName();
        // On update le compte
        Compte compte = compteService.updateCompte(pseudo);

        return ResponseEntity.ok(compte); // On renvoie le compte existant
    } 


    // Détruire le compte
    @PreAuthorize("isAuthenticated()")
    @DeleteMapping
    public ResponseEntity<Void> deleteCompte(Authentication authentication){
        try {
            // Récupérer le nom d'utilisateur de l'authentification (car la méthode deleteCompte prend un String)
            String pseudo = authentication.getName();
            // On supprime le compte
            compteService.deleteCompte(pseudo);
            return ResponseEntity.ok().build(); // On renvoie le message de confirmation
        } catch (IllegalArgumentException e) {
            // Si le pseudo n'existe pas, on renvoie une erreur
            return ResponseEntity.notFound().build();
        }
    } 
    
}

/*
GET /comptes/{id} Obtenir les infos du compte
PUT /comptes/{id} Mettre à jour 
DELETE /comptes/{id} Détruire le compte
 */