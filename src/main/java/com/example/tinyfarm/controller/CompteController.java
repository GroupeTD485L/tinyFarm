/*package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Compte;
import  com.example.tinyfarm.service.CompteService;

@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/comptes/{id}")
public class CompteController {
    
    private final CompteService compteService;

    public CompteController(CompteService compteService){
        this.CompteService = compteService;
    }

    @PostMapping
    public void creerCompte(){}

    @GetMapping
    public Commerce infoCompte(){}

    @PutMapping
    public void updateCompte(){} 

    @DeleteMapping
    public void deleteCompte(){} 
    
}
*/