package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import  com.example.tinyfarm.entity.Clapier;
import  com.example.tinyfarm.service.ClapierService;


@RestController 
@RequestMapping("/compte/{idFerme}/clapier") // URL
public class ClapierController {
    
    private final ClapierService clapierService; 


    // Constructeur du Controller
    public ClapierController(ClapierService clapierService){
        this.clapierService = clapierService;
    }


    // Créer le clapier TODO /!\ VOIR LE CORPS DE CLAPIERSERVICE.CREERCLAPIER
    @PreAuthorize("isAuthenticated()")
    @PostMapping
    public ResponseEntity<Clapier> creerClapier(@PathVariable Long idFerme){ 
        Clapier clapier = clapierService.creerClapier(idFerme); // Crée le clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie le clapier créé
        } else {
            // Si le clapier n'a pas pu être créé
            return ResponseEntity.badRequest().build();
        }
    }  


    // Obtenir les infos du clapier 
    @PreAuthorize("isAuthenticated()")
    @GetMapping
    public ResponseEntity<Clapier> getClapier(@PathVariable Long fermeId) {
        Clapier clapier = clapierService.getInfoClapier(fermeId); // Récupére les infos du clapier cible
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos modifiées du clapier
        } else {
            // Si le clapier est inexistant
             return ResponseEntity.notFound().build();
        }
    }


    // Met à jour les infos du clapier
    @PreAuthorize("isAuthenticated()")
    @PutMapping 
    public ResponseEntity<Clapier> updateClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.updateClapier(fermeId); // Met à jour les infos du clapier
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
    public ResponseEntity<Clapier> nourrirClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.nourrirClapier(fermeId); // Met à jour les infos du clapier
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
    public ResponseEntity<Clapier> abreuverClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.abbreuverClapier(fermeId); // Met à jour les infos du clapier
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
    public ResponseEntity<Clapier> soignerClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.SoignerClapier(fermeId); // Met à jour les infos du clapier
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
    public ResponseEntity<Clapier> laverClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.laverClapier(fermeId); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    // Supprime le clapier de la ferme
    @PreAuthorize("isAuthenticated()")
    @PutMapping("/supprimer")
    public ResponseEntity<Void> detruireClapier(@PathVariable Long fermeId){
        // On doit gérer une exception (car renvoie un void), si le clapier existe, ou pas
        try {
            clapierService.supprimerClapier(fermeId);
            return ResponseEntity.ok().build(); // Le clapier a été supprimé correctement
        } catch (Exception e) {
            return ResponseEntity.badRequest().build(); // Si le clapier n'a pas pu être supprimé
        }
    }
} 

