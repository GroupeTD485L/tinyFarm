/*package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Poule;
import  com.example.tinyfarm.service.PouleService;

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{id}/ferme/{id}/poulailler")
public class PouleController {
    
    private final PouleService pouleService;
    private final FermeService fermeService;

    public VacheController(PouleService pouleService, FermeService fermeService){
        this.fermeService = fermeService;
        this.pouleService = pouleService;
    }

    @PostMapping
    public void creerPoule(){}

    @GetMapping
    public Poule getListeVolailles(){}

    // Gestion des volailles de type coqs

    @GetMapping("/coq")
    public Poule getListeCoqs(){}

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
    public Poule getListePoules(){}

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
    public Poule getListePoussins(){}

    @PutMapping("/poussins/nourrir")
    public void nourrirPoussins(){} 

    @PutMapping("/poussins/abreuver")
    public void abreuverPoussins(){} 

    @PutMapping("/poussins/soigner")
    public void soignerPoussins(){} 

    @PutMapping("/poussins/laver")
    public void laverPoussins(){} 

    // Gestion d'un type de volaille donné

    @GetMapping("/{id}")
    public Poule getPoule(){}

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
*/