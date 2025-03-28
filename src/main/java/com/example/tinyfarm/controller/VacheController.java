package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;


import  com.example.tinyfarm.entity.Vache;
import  com.example.tinyfarm.service.VacheService;

@RestController
@RequestMapping("/compte/{idFerme}/vache")
public class VacheController {

    private final VacheService vacheService;

    public VacheController(VacheService vacheService){
        this.vacheService = vacheService;
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
    public ResponseEntity<Vache> getVache(@PathVariable Long idFerme){
        Vache vache = vacheService.getInfoCow(idFerme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> updateVache(@PathVariable Long idFerme){
        Vache vache = vacheService.updateVache(idFerme);
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
    public ResponseEntity<Vache> nourrirVache(@PathVariable Long idFerme){
        Vache vache = vacheService.updateVache(idFerme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/abreuver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> abreuverVache(@PathVariable Long idFerme){
        Vache vache = vacheService.updateVache(idFerme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/soigner")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> soignerVache(@PathVariable Long idFerme){
        Vache vache = vacheService.soignerVache(idFerme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/laver")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Vache> laverVache(@PathVariable Long idFerme){
        Vache vache = vacheService.laverVache(idFerme);
        if (vache != null){
            return ResponseEntity.ok(vache);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
