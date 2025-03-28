/*package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Clapier;
import  com.example.tinyfarm.service.ClapierService;

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{id}/ferme/{id}/clapier")
public class ClapierController {
    
    private final ClapierService clapierService;
    private final FermeService fermeService;

    public VacheController(ClapierService clapierService, FermeService fermeService){
        this.fermeService = fermeService;
        this.clapierService = clapierService;
    }

    @GetMapping
    public Clapier getClapier(){}

    @PutMapping
    public void updateClapier(){} 

    @DeleteMapping
    public void deleteClapier(){} 

    @PutMapping("/nourrir")
    public void nourrirClapier(){}

    @PutMapping("/abreuver")
    public void abreuverClapier(){}

    @PutMapping("/soigner")
    public void soignerClapier(){}

    @PutMapping("/laver")
    public void laverClapier(){}

}*/
