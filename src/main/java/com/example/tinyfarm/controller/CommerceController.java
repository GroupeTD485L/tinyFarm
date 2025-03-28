package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Commerce;
import  com.example.tinyfarm.service.CommerceService;
import  com.example.tinyfarm.repository.CommerceRepository;
import  com.example.tinyfarm.entity.Compte;
import  com.example.tinyfarm.service.CompteService;



@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{idFerme}/commerce")
public class CommerceController {
    
    private final CommerceService commerceService;
    private final CommerceRepository commerceRepository;
    private final FermeService fermeService;
    private final CompteService compteService;

    public CommerceController(CompteService compteService, FermeService fermeService, CommerceService commerceService, CommerceRepository commerceRepository){
        this.commerceService = commerceService;
        this.fermeService = fermeService;
        this.compteService = compteService;
        this.commerceRepository = commerceRepository;
    }

    @PostMapping
    public ResponseEntity<Commerce> creerCommerce(@PathVariable long idFerme, @RequestBody Commerce commerce){
        Commerce c = commerceService.addComerce(commerce);
        if (c != null){
            return ResponseEntity.ok(c);
        } else {
            return ResponseEntity.notFound().build();
        }

    }
    /* TODO
    @GetMapping("/{id}")
    public Commerce infoCommerce(){}

    @PutMapping("/{id}")
    public void updateCommerce(){} 

    @GetMapping("/eleveurs")
    public void getInfoVenteNonFini(){
        return
    }

    @GetMapping("/coop")
    public void getInfoCoop(){}
    
    */
}
