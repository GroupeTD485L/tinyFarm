package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Poule;
import  com.example.tinyfarm.service.PouleService;
import  com.example.tinyfarm.repository.PouleRepository;


import java.util.Optional;


@RestController
@RequestMapping("/compte/{idFerme}/poulailler")
public class PouleController {
    
    private final PouleService pouleService;
    private final FermeService fermeService;
    private final PouleRepository pouleRepository;

    public PouleController(PouleService pouleService, FermeService fermeService, PouleRepository pouleRepository){
        this.fermeService = fermeService;
        this.pouleService = pouleService;
        this.pouleRepository = pouleRepository;
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> creerPoule(@PathVariable long idFerme, @RequestBody Poule poule){
        poule.setProprietaire(fermeService.getFerme(idFerme));
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

    // Gestion des volailles de type coq 
    @GetMapping("/coqs")
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListeCoqs(@PathVariable long idFerme, Pageable pageable){
        return pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme) , 'M', pageable);
    }

    @PutMapping("/coqs/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> nourrirCoqs(@PathVariable long idFerme,@RequestBody String nourriture , Pageable pageable){
        Page<Poule> allCoqs = pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme) , 'M', pageable);
        for (Poule c : allCoqs){
            if (c == null){ 
                return ResponseEntity.notFound().build();
            }
            pouleService.nourrirPoule(c.getIdPoule(), nourriture);
        }
        return ResponseEntity.ok(allCoqs);
    } 
    
    @PutMapping("/coqs/abreuver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> abreuverCoqs(@PathVariable long idFerme,@RequestBody String nourriture , Pageable pageable){
        Page<Poule> allCoqs = pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme) , 'M', pageable);
        for (Poule c : allCoqs){
            if (c == null){ 
                return ResponseEntity.notFound().build();
            }
            pouleService.abreuverPoule(c.getIdPoule(), nourriture);
        }
        return ResponseEntity.ok(allCoqs);
    } 

    // Gestion des volailles de type poule

    @GetMapping("/poules")
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListePoules(@PathVariable long idFerme, Pageable pageable){
        return pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme), 'F', pageable);
    }

    @PutMapping("/poules/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> nourrirPoules(@PathVariable long idFerme,@RequestBody String nourriture , Pageable pageable){
        Page<Poule> allPoules = pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme), 'F', pageable);
        for (Poule p : allPoules){
            if (p == null){ 
                return ResponseEntity.notFound().build();
            }
            pouleService.nourrirPoule(p.getIdPoule(), nourriture);
        }
        return ResponseEntity.ok(allPoules);
    } 

    @PutMapping("/poules/abreuver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> abreuverPoules(@PathVariable long idFerme,@RequestBody String nourriture , Pageable pageable){
        Page<Poule> allPoules = pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme), 'F', pageable);
        for (Poule p : allPoules){
            if (p == null){ 
                return ResponseEntity.notFound().build();
            }
            pouleService.abreuverPoule(p.getIdPoule(), nourriture);
        }
        return ResponseEntity.ok(allPoules);    
    } 

    // Gestion des volailles de type poussin

    @GetMapping("/poussins")
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListePoussins(@PathVariable long idFerme, Pageable pageable){
        return pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme), 'U', pageable); 
    }

    @PutMapping("/poussins/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> nourrirPoussins(@PathVariable long idFerme,@RequestBody String nourriture , Pageable pageable){
        Page<Poule> allPoussins = pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme), 'U', pageable);
        for (Poule p : allPoussins){
            if (p == null){
                return ResponseEntity.notFound().build();
            }
            pouleService.nourrirPoule(p.getIdPoule(), nourriture);
        }
        return ResponseEntity.ok(allPoussins);
    } 

    @PutMapping("/poussins/abreuver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> abreuverPoussins(@PathVariable long idFerme,@RequestBody String nourriture , Pageable pageable){
        Page<Poule> allPoussins = pouleService.getPoulesByProprietaireAndSexe(fermeService.getFerme(idFerme), 'U', pageable);
        for (Poule p : allPoussins){
            if (p == null){
                return ResponseEntity.notFound().build();
            }
            pouleService.abreuverPoule(p.getIdPoule(), nourriture);
        }
        return ResponseEntity.ok(allPoussins);
    } 

    // Méthode d'update 
    @PutMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> updatePoulailler(@PathVariable long idFerme, Pageable pageable){
        Page<Poule> allPoule = pouleRepository.findAllByProprietaire(fermeService.getFerme(idFerme), pageable);
        for (Poule p : allPoule){
            if (p == null){ 
                return ResponseEntity.notFound().build();
            }
            pouleService.updatePoule(p.getIdPoule());
        }
        return ResponseEntity.ok(allPoule);
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
    public ResponseEntity<Poule> nourrirVolaille(@PathVariable long idPoule, @RequestBody String nourriture){
        Poule poule = pouleService.nourrirPoule(idPoule, nourriture);
        if (poule != null){
            return ResponseEntity.ok(poule);
        } else {
            return ResponseEntity.notFound().build();
        }
    } 

    @PutMapping("/{idPoule}/abreuver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> abreuverVolaille(@PathVariable long idPoule, @RequestBody String nourriture){
        Poule poule = pouleService.abreuverPoule(idPoule, nourriture);
        if (poule != null){
            return ResponseEntity.ok(poule);
        } else {
            return ResponseEntity.notFound().build();
        }
    } 

    @PutMapping("/{idPoule}/soigner")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> soignerVolaille(@PathVariable long idPoule){
        Poule poule = pouleService.soignerPoule(idPoule);
        if (poule != null){
            return ResponseEntity.ok(poule);
        } else {
            return ResponseEntity.notFound().build();
        }
    } 

    @PutMapping("/{idPoule}/laver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Poule> laverVolaille(@PathVariable long idPoule){
        Poule poule = pouleService.laverPoule(idPoule);
        if (poule != null){
            return ResponseEntity.ok(poule);
        } else {
            return ResponseEntity.notFound().build();
        }
    } 


    /* Pas logique qu'un utilisateur puisse delete son clapier
    @DeleteMapping
    public void deletePoulailler(){} 
    */
}
