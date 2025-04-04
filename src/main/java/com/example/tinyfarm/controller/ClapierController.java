package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;

import com.example.tinyfarm.entity.Clapier;
import com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.service.FermeService;
import com.example.tinyfarm.service.ClapierService;
import org.springframework.web.bind.annotation.PutMapping;


@RestController 
@RequestMapping("/ferme/clapier") // URL
public class ClapierController {

    private final FermeService fermeService;
    
    private final ClapierService clapierService; 

    // Constructeur du Controller
    public ClapierController(ClapierService clapierService, FermeService fermeService){
        this.clapierService = clapierService;
        this.fermeService = fermeService;
    }

    // Création du clapier non utile car déjà fait dans la création de la ferme

    // Obtenir les infos du clapier 
    @PreAuthorize("isAuthenticated()")
    @GetMapping
    public ResponseEntity<Clapier> getClapier(Authentication authentication) {
        String pseudo = authentication.getName(); // Récupérer le nom d'utilisateur de l'authentification
        Clapier clapier = clapierService.getInfoClapier(pseudo); // Récupére les infos du clapier cible
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos modifiées du clapier
        } else {
            // Si le clapier est inexistant
             return ResponseEntity.notFound().build();
        }
    }


    @Scheduled(cron="0 0 0 * * ?")
    public void scheduleUpdateAllClapier(){
        clapierService.updateAllClapier();
    }

    @PutMapping("admin/updateAllClapier")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> updateAllClapier() {
        try {
            clapierService.updateAllClapier();
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    }

    @PutMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Clapier> updateClapier(Authentication authentication){
        //String pseudo = authentication.getName();
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Clapier clapier = clapierService.updateClapier(ferme); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos modifiées du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }  


    // Nourrir les membres du clapier
    @PreAuthorize("isAuthenticated()")
    @PutMapping("/nourrir")
    public ResponseEntity<Clapier> nourrirClapier(Authentication authentication){
        String pseudo = authentication.getName();
        Clapier clapier = clapierService.nourrirClapier(pseudo); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos modifiées du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    // Abreuver les membres du clapier
    @PreAuthorize("isAuthenticated()")
    @PutMapping("/abreuver")
    public ResponseEntity<Clapier> abreuverClapier(Authentication authentication){
        String pseudo = authentication.getName();
        Clapier clapier = clapierService.abbreuverClapier(pseudo); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos modifiées du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    // Soigner les membres du clapier
    @PreAuthorize("isAuthenticated()")
    @PutMapping("/soigner")
    public ResponseEntity<Clapier> soignerClapier(Authentication authentication){
        String pseudo = authentication.getName();
        Clapier clapier = clapierService.SoignerClapier(pseudo); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos modifiées du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    // Laver les membres du clapier
    @PreAuthorize("isAuthenticated()")
    @PutMapping("/laver")
    public ResponseEntity<Clapier> laverClapier(Authentication authentication){
        String pseudo = authentication.getName();
        Clapier clapier = clapierService.laverClapier(pseudo); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    /* 
    // Supprime le clapier de la ferme
    @PreAuthorize("isAuthenticated()")
    @PutMapping("/supprimer")
    public ResponseEntity<Void> detruireClapier(Authentification authentification){
        String pseudo = authentication.getName();
        // On doit gérer une exception (car renvoie un void), si le clapier existe, ou pas
        try {
            clapierService.supprimerClapier(pseudo);
            return ResponseEntity.ok().build(); // Le clapier a été supprimé correctement
        } catch (Exception e) {
            return ResponseEntity.badRequest().build(); // Si le clapier n'a pas pu être supprimé
        }
    }
     */
} 

