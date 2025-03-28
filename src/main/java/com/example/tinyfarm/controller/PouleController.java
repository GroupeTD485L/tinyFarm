package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Poule;
import  com.example.tinyfarm.service.PouleService;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PathVariable;


@RestController
@RequestMapping("/compte/{idFerme}/poulailler")
public class PouleController {
    
    private final PouleService pouleService;
    private final FermeService fermeService;

    public PouleController(PouleService pouleService, FermeService fermeService){
        this.fermeService = fermeService;
        this.pouleService = pouleService;
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> creerPoule(@PathVariable long idFerme, @RequestBody Poule poule){
        //poule.setProprietaire(fermeService.getOrCreateFermeForUser(null));  TODO : Besoin d'une méthode pour trouver une ferme à partir de l'id 
        Poule pouleAdded = pouleService.addPoule(poule);
        if(pouleAdded != null){
            return ResponseEntity.ok(pouleAdded);
        } else {
            return ResponseEntity.notFound().build();
        }

    }

    @GetMapping
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListeVolailles(Pageable pageable){
        return pouleService.getAllPoules(pageable);
    }

    // Gestion des volailles de type coqs
    // TODO : avec les nouvelles méthodes de PouleService 
    @GetMapping("/coqs")
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListeCoqs(Pageable pageable){
        return pouleService.getPoulesByProprietaireAndSexe(null, 'M', pageable); // TODO : méthode qui donne la ferme en fonction de l'id
    }

    @PutMapping("/coqs/nourrir")
    @PreAuthorize("isAuthenticated()")
    public void nourrirCoqs(){} 

    @PutMapping("/coqs/abreuver")
    @PreAuthorize("isAuthenticated()")
    public void abreuverCoqs(){} 

    // Gestion des volailles de type poule

    @GetMapping("/poules")
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListePoules(Pageable pageable){
        return pouleService.getPoulesByProprietaireAndSexe(null, 'F', pageable);  // TODO : méthode qui donne la ferme en fonction de l'id
    }

    @PutMapping("/poules/nourrir")
    @PreAuthorize("isAuthenticated()")
    public void nourrirPoules(){} 

    @PutMapping("/poules/abreuver")
    @PreAuthorize("isAuthenticated()")
    public void abreuverPoules(){} 

    // Gestion des volailles de type poussin

    @GetMapping("/poussins")
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListePoussins(Pageable pageable){
        return pouleService.getPoulesByProprietaireAndSexe(null, 'U', pageable);  // TODO : méthode qui donne la ferme en fonction de l'id
    }

    @PutMapping("/poussins/nourrir")
    @PreAuthorize("isAuthenticated()")
    public void nourrirPoussins(){} 

    @PutMapping("/poussins/abreuver")
    @PreAuthorize("isAuthenticated()")
    public void abreuverPoussins(){} 

    // Méthode d'update 

    @PutMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> updatePoulailler(@PathVariable long idFerme, Pageable pageable){

    } 

    // Gestion d'un type de volaille donné

    @GetMapping("/{idPoule}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> getPoule(@PathVariable long idPoule){
        Optional<Poule> poule = pouleService.getPouleById(idPoule);
        if (poule != null){
            Poule p = poule.get();
            return ResponseEntity.ok(p);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/{idPoule}/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> nourrirVolaille(){} 

    @PutMapping("/{idPoule}/abreuver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> abreuverVolaille(){} 

    @PutMapping("/{idPoule}/soigner")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> soignerVolaille(){} 

    @PutMapping("/{idPoule}/laver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> laverVolaille(){} 


    /* Pas logique qu'un utilisateur puisse delete son clapier
    @DeleteMapping
    public void deleteClapier(){} 
    */
}
