package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;


import  com.example.tinyfarm.entity.Vache;
import com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.service.VacheService;
import org.springframework.web.bind.annotation.PutMapping;

@RestController
@RequestMapping("/vache")
public class VacheController {

    private final FermeService fermeService;

    private final VacheService vacheService;

    public VacheController(VacheService vacheService, FermeService fermeService){
        this.vacheService = vacheService;
        this.fermeService = fermeService;
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> createVache(){
        Vache vache = vacheService.createCow();
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> getVache(Authentication authentication){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.getInfoCow(ferme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @Scheduled(cron="0 0 0 * * ?")
    public void scheduleUpdateAllVache(){
        vacheService.updateAllVache();
    }

    @PutMapping("admin/updateAllVache")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> updateAllVache() {
        try {
            vacheService.updateAllVache();
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    }

    //update de la vache en fin de journee
    @PutMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> updateVache(Authentication authentication){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.updateVache(ferme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    //update de la production de lait de la vache
    @Scheduled(cron="0 0 6,18 * * ?")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> updateLaitVache(Authentication authentication){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.updateLaitVache(ferme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    } 

    
/*  Plutôt en tant que Service à utiliser lorsque la vache meurt
    @DeleteMapping("/kill")
    @PreAuthorize("isAuthenticated()")
    public void deleteVache(){

    } 
*/
    @PutMapping("/nourrir")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> nourrirVache(Authentication authentication, @RequestBody String nomProduit){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.nourrirVache(ferme,nomProduit);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/abreuver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> abreuverVache(Authentication authentication){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.abreuverVache(ferme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/soigner")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> soignerVache(Authentication authentication){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.soignerVache(ferme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/laver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> laverVache(Authentication authentication){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.laverVache(ferme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/faireMalade")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> faireMaladeVache(Authentication authentication){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Vache vache = vacheService.faireMalade(ferme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
}
