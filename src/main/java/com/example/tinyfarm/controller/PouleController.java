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

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{idFerme}/poulailler")
public class PouleController {
    
    private final PouleService pouleService;
    private final FermeService fermeService;

    public PouleController(PouleService pouleService, FermeService fermeService){
        this.fermeService = fermeService;
        this.pouleService = pouleService;
    }

    @PostMapping
    public ResponseEntity<Poule> creerPoule(@PathVariable long idFerme, @RequestBody Poule poule){
        poule.setProprietaire(fermeService.getOrCreateFermeForUser(null)); // TODO : Besoin d'une méthode pour trouver une ferme à partir de l'id 
        Poule pouleAdded = pouleService.addPoule(poule);
        if(pouleAdded != null){
            return ResponseEntity.ok(pouleAdded);
        } else {
            return ResponseEntity.notFound().build();
        }

    }

    @GetMapping
    public Page<Poule> getListeVolailles(Pageable pageable){
        return pouleService.getAllPoules(pageable);
    }

    // Gestion des volailles de type coqs
    // TODO : avec les nouvelles méthodes de PouleService 
    @GetMapping("/coq")
    public Page<Poule> getListeCoqs(Pageable pageable){}

    @PutMapping("/coq/nourrir")
    public void nourrirCoqs(){} 

    @PutMapping("/coq/abreuver")
    public void abreuverCoqs(){} 

    @PutMapping("/coq/soigner")
    public void soignerCoqs(){} 

    @PutMapping("/coq/laver")
    public void laverCoqs(){} 

    // Gestion des volailles de type poule

    @GetMapping("/poules")
    public Page<Poule> getListePoules(Pageable pageable){}

    @PutMapping("/poules/nourrir")
    public void nourrirPoules(){} 

    @PutMapping("/poules/abreuver")
    public void abreuverPoules(){} 

    @PutMapping("/poules/soigner")
    public void soignerPoules(){} 

    @PutMapping("/poules/laver")
    public void laverPoules(){} 

    // Gestion des volailles de type poussin

    @GetMapping("/poussins")
    public Page<Poule> getListePoussins(Pageable pageable){}

    @PutMapping("/poussins/nourrir")
    public void nourrirPoussins(){} 

    @PutMapping("/poussins/abreuver")
    public void abreuverPoussins(){} 

    @PutMapping("/poussins/soigner")
    public void soignerPoussins(){} 

    @PutMapping("/poussins/laver")
    public void laverPoussins(){} 

    // Gestion d'un type de volaille donné

    @GetMapping("/{idPoule}")
    public ResponseEntity<Poule> getPoule(@PathVariable long idPoule){
        Optional<Poule> poule = pouleService.getPouleById(idPoule);
        if (poule != null){
            Poule p = poule.get();
            return ResponseEntity.ok(p);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/{id}")
    public void updatePoule(){} 

    @PutMapping("/{id}/nourrir")
    public void nourrirVolaille(){} 

    @PutMapping("/{id}/abreuver")
    public void abreuverVolaille(){} 

    @PutMapping("/{id}/soigner")
    public void soignerVolaille(){} 

    @PutMapping("/{id}/laver")
    public void laverVolaille(){} 





    @DeleteMapping
    public void deleteClapier(){} 

}
