package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import  com.example.tinyfarm.entity.Clapier;
import  com.example.tinyfarm.service.ClapierService;


@RestController 
@PreAuthorize("isAuthenticated()") // L'utilisateur doit être authentifié
@RequestMapping("/comptes/fermes/{fermeId}/clapier") // URL
public class ClapierController {
    
    private final ClapierService clapierService; 


    // Constructeur du Controller
    public ClapierController(ClapierService clapierService){
        this.clapierService = clapierService;
    }


    // Créer le clapier TODO /!\ VOIR LE CORPS DE CLAPIERSERVICE.CREERCLAPIER
    // @PreAuthorize("hasRole('ROLE_ADMIN')") // L'utilisateur doit être un admin   
    @PostMapping
    public ResponseEntity<Clapier> creerClapier(@PathVariable Long idFerme){ // Créer le clapier 
        Clapier clapier = clapierService.creerClapier(idFerme); // Créer le clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie le clapier créé
        } else {
            // Si le clapier n'a pas pu être créé
            return ResponseEntity.badRequest().build();
        }
    }  


    // Obtenir les infos du clapier 
    @GetMapping
    public ResponseEntity<Clapier> getClapier(@PathVariable Long fermeId) {
        Clapier clapier = clapierService.getInfoClapier(fermeId); // Récupére les infos du clapier cible
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos du clapier
        } else {
            // Si le clapier est inexistant
             return ResponseEntity.notFound().build();
        }
    }


    // Met à jour les infos du clapier
    @PutMapping 
    public ResponseEntity<Clapier> updateClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.updateClapier(fermeId); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }  


    // Nourrir les membres du clapier
    @PutMapping("/nourrir")
    public ResponseEntity<Clapier> nourrirClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.nourrirClapier(fermeId); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    // Abreuver les membres du clapier
    @PutMapping("/abreuver")
    public ResponseEntity<Clapier> abreuverClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.abbreuverClapier(fermeId); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    // Soigner les membres du clapier
    @PutMapping("/soigner")
    public ResponseEntity<Clapier> soignerClapier(@PathVariable Long fermeId){
        Clapier clapier = clapierService.SoignerClapier(fermeId); // Met à jour les infos du clapier
        if(clapier != null) {
            return ResponseEntity.ok(clapier); // On renvoie les infos du clapier
        } else {
            // Si le clapier n'a pas pu être mis à jour
            return ResponseEntity.badRequest().build();
        }
    }


    // Laver les membres du clapier
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


/* COMMENT ???
    // Supprime le clapier de la ferme
    @DeleteMapping
    public ResponseEntity<Clapier>id deleteClapier(){

    } 
*/

}

/*
POST      /comptes/fermes/{fermeId}/clapier  Créer le clapier
GET        /comptes/fermes/{fermeId}/clapier Obtenir les infos du clapier

PUT         /comptes/fermes/{fermeId}/clapier Update les infos du clapier
PUT         /comptes/fermes/{fermeId}/clapier/nourrir Nourrit les membres du clapier
PUT        /comptes/fermes/{fermeId}/clapier/abreuver Abreuver les membres du clapier
PUT        /comptes/fermes/{fermeId}/clapier/soigner Soigner les membres du clapier
PUT        /comptes/fermes/{fermeId}/clapier/laver Laver les membres du clapier

DELETE /comptes/{id}/fermes/clapier Detruire le clapîer de la ferme
*/
