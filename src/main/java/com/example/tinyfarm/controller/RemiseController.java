/*package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Commerce;
import  com.example.tinyfarm.service.CommerceService;
import  com.example.tinyfarm.entity.Compte;
import  com.example.tinyfarm.service.CompteService;

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{id}/fermes/{id}/remise")
public class RemiseController {
    
    private final RemiseService remiseService;
    private final FermeService fermeService;
    private final CompteService compteService;

    public CommerceController(CompteService compteService, FermeService fermeService, RemiseService remiseService){
        this.remiseService = remiseService;
        this.fermeService = fermeService;
        this.compteService = compteService;
    }

    @PostMapping
    public void rajouterProduit(){}

    @GetMapping
    public Remise infoRemise(){}

    @GetMapping("/{id}")
    public Produit infoProduit(){}

    @PutMapping("/{id}")
    public void updateProduit(){} 

    @DeleteMapping
    public void deleteRemise(){} 

}
*/