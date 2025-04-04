package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;

@RestController
@RequestMapping("/ferme/") // URL
public class FermeController {

    private final FermeService fermeService;

    public FermeController(FermeService fermeService) {
        this.fermeService = fermeService;
    }


    // Créer une ferme (nouveau joueur)
    @PreAuthorize("isAuthenticated()")
    @PostMapping
    public ResponseEntity<Ferme> createFerme(Authentication authentication) {
        // Récupérer le nom d'utilisateur de l'authentification (car la méthode getOrCreateFermeForUser prend un String)
        String pseudo = authentication.getName();
        // On crée la ferme
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);

        return ResponseEntity.ok(ferme); // On renvoie la ferme créée
    }


    // Get une ferme
    @PreAuthorize("isAuthenticated()")
    @GetMapping
    public ResponseEntity<Ferme> getFerme(Authentication authentication) {
        // Récupérer le nom d'utilisateur de l'authentification (car la méthode getOrCreateFermeForUser prend un String)
        String pseudo = authentication.getName();
        // On get la ferme
        Ferme ferme = fermeService.getOrCreateFermeForUser(pseudo);

        return ResponseEntity.ok(ferme); // On renvoie la ferme existante
    }


    // Mettre à jour une ferme
    @PreAuthorize("isAuthenticated()")
    // @Scheduled(cron="0 0 0 * * ?")
    @PutMapping
    public ResponseEntity<Ferme> updateFerme(Authentication authentication) {
        // Récupérer le nom d'utilisateur de l'authentification (car la méthode updateFerme prend un String)
        String pseudo = authentication.getName();
        // On update la ferme
        Ferme ferme = fermeService.updateFerme(pseudo);

        return ResponseEntity.ok(ferme); // On renvoie la ferme modifiée
    }

    // Supprimer une ferme
    @PreAuthorize("isAuthenticated()")
    @DeleteMapping
    public ResponseEntity<Void> deleteFerme(Authentication authentication) {
        // On doit gérer une exception (car renvoie un void), si la ferme existe, ou pas
        try {
            // Récupére le nom d'utilisateur de l'authentification (car la méthode deleteFerme prend un String)
            String pseudo = authentication.getName();
            // On supprime la ferme
            fermeService.deleteFerme(pseudo);
            return ResponseEntity.ok().build(); // On renvoie le message de confirmation
        } catch (IllegalArgumentException e) {
            // Si le pseudo n'existe pas, on renvoie une erreur
            return ResponseEntity.notFound().build();
        }
    }
}