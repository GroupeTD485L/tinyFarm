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
@RequestMapping("/compte/{id}/fermes/{id}/commerce")
public class CommerceController {
    
    private final CommerceService commerceService;
    private final FermeService fermeService;
    private final CompteService compteService;

    public CommerceController(CompteService compteService, FermeService fermeService, CommerceService commerceService){
        this.commerceService = commerceService;
        this.fermeService = fermeService;
        this.compteService = compteService;
    }

    @PostMapping
    public void creerCommerce(){}

    @GetMapping("/{id}")
    public Commerce infoCommerce(){}

    @PutMapping("/{id}")
    public void updateCommerce(){} 

    @DeleteMapping
    public void deleteCommerce(){} 

}
*/