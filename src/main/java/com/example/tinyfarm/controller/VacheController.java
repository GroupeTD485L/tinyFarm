/*
package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Vache;
import  com.example.tinyfarm.service.VacheService;

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{id}/ferme/{id}/vache")
public class VacheController {

    private final VacheService vacheService;
    private final FermeService fermeService;

    public VacheController(VacheService vacheService, FermeService fermeService){
        this.fermeService = fermeService;
        this.vacheService = vacheService;
    }

    @GetMapping
    public Vache getVache(){}

    @PutMapping
    public void updateVache(){} 

    @DeleteMapping
    public void deleteVache(){} 

    @PutMapping("/nourrir")
    public void nourrirVache(){}

    @PutMapping("/abreuver")
    public void abreuverVache(){}

    @PutMapping("/soigner")
    public void soignerVache(){}

    @PutMapping("/laver")
    public void laverVache(){}
}
*/