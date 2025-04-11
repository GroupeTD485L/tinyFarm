package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.scheduling.annotation.Scheduled;



import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Poule;
import  com.example.tinyfarm.service.PouleService;
import  com.example.tinyfarm.repository.PouleRepository;


import java.util.Optional;

//ajout
import java.io.PrintWriter;
import java.io.StringWriter;
// Ajoutez cet import en haut du fichier
import org.springframework.data.domain.PageRequest;

@RestController
@RequestMapping("/poulailler")
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
    public ResponseEntity<Poule> creerPoule(Authentication authentication, @RequestBody Poule poule){
        String pseudo = authentication.getName();
        poule.setProprietaire(fermeService.getOrCreateFermeForUser(pseudo));
        Poule pouleAdded = pouleService.addPoule(poule);
        if(pouleAdded != null){
            return ResponseEntity.ok(pouleAdded);
        } else {
            return ResponseEntity.notFound().build();
        }

    }

    @GetMapping
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListeVolailles(Authentication authentication, Pageable pageable){
        String pseudo = authentication.getName();
        return pouleService.getAllMyPoules(fermeService.getOrCreateFermeForUser(pseudo), pageable);
    }

    // Gestion des volailles de type coq 
    @GetMapping("/coqs")
    @PreAuthorize("isAuthenticated()")
    public Page<Poule> getListeCoqs(Authentication authentication, Pageable pageable){
        String pseudo = authentication.getName();
        return pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo) , 'M', pageable);
    }

    @PutMapping("/coqs/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> nourrirCoqs(Authentication authentication,@RequestBody String nourriture , Pageable pageable){
        String pseudo = authentication.getName();
        Page<Poule> allCoqs = pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo) , 'M', pageable);
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
    public ResponseEntity<Page<Poule>> abreuverCoqs(Authentication authentication, @RequestBody String nourriture , Pageable pageable){
        String pseudo = authentication.getName();
        Page<Poule> allCoqs = pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo), 'M', pageable);
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
    public Page<Poule> getListePoules(Authentication authentication, Pageable pageable){
        String pseudo = authentication.getName();
        return pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo), 'F', pageable);
    }

    @PutMapping("/poules/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> nourrirPoules(Authentication authentication,@RequestBody String nourriture , Pageable pageable){
        String pseudo = authentication.getName();
        Page<Poule> allPoules = pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo), 'F', pageable);
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
    public ResponseEntity<Page<Poule>> abreuverPoules(Authentication authentication, @RequestBody String nourriture , Pageable pageable){
        String pseudo = authentication.getName();
        Page<Poule> allPoules = pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo), 'F', pageable);
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
    public Page<Poule> getListePoussins(Authentication authentication, Pageable pageable){
        String pseudo = authentication.getName();
        return pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo), 'U', pageable); 
    }

    @PutMapping("/poussins/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Poule>> nourrirPoussins(Authentication authentication, @RequestBody String nourriture , Pageable pageable){
        String pseudo = authentication.getName();
        Page<Poule> allPoussins = pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo), 'U', pageable);
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
    public ResponseEntity<Page<Poule>> abreuverPoussins(Authentication authentication, @RequestBody String nourriture , Pageable pageable){
        String pseudo = authentication.getName();
        Page<Poule> allPoussins = pouleService.getPoulesByProprietaireAndSexe(fermeService.getOrCreateFermeForUser(pseudo), 'U', pageable);
        for (Poule p : allPoussins){
            if (p == null){
                return ResponseEntity.notFound().build();
            }
            pouleService.abreuverPoule(p.getIdPoule(), nourriture);
        }
        return ResponseEntity.ok(allPoussins);
    } 
    
    @Scheduled(cron="0 0 0 * * ?")
    public void scheduleUpdateAllPoulailler(){
        pouleService.updateAllPoules();
    }

    @PutMapping("admin/updateAllPoulailler")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<String> updateAllPoulailler() {
        try {
            pouleService.updateAllPoules();
            return ResponseEntity.ok("Mise à jour réussie");
        } catch (Exception e) {
            e.printStackTrace(); // Affiche la pile d'appels dans les logs
            return ResponseEntity.status(500).body("Erreur : " + e.getMessage() + "\n" + e.getClass().getName());
        }
    }

    // Méthode d'update 
    @PreAuthorize("isAuthenticated()")
    @PutMapping
    public ResponseEntity<Page<Poule>> updatePoulailler(Authentication authentication, Pageable pageable){
        String pseudo = authentication.getName();
        Page<Poule> allPoule = pouleRepository.findAllByProprietaire(fermeService.getOrCreateFermeForUser(pseudo), pageable);
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
    // Ajout d'une méthode pour rendre une poule malade
    @PutMapping("/{idPoule}/rendreMalade")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Poule> rendreMaladeVolaille(@PathVariable long idPoule) {
    // Sans utiliser Authentication, puisque c'est un admin
        Poule poule = pouleService.rendreMaladePoule(idPoule, null);  // null pour le paramètre ferme
        if (poule != null) {
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
