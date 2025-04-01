package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;
import  com.example.tinyfarm.entity.Commerce;
import  com.example.tinyfarm.service.CommerceService;
import  com.example.tinyfarm.repository.CommerceRepository;
import  com.example.tinyfarm.service.CompteService;



@RestController
@PreAuthorize("isAuthenticated()")
@RequestMapping("/compte/{idFerme}/commerce")
public class CommerceController {
    
    private final CommerceService commerceService;
    private final CommerceRepository commerceRepository;
    private final FermeService fermeService;

    public CommerceController(CompteService compteService, FermeService fermeService, CommerceService commerceService, CommerceRepository commerceRepository){
        this.commerceService = commerceService;
        this.fermeService = fermeService;
        this.commerceRepository = commerceRepository;
    }

    @PostMapping
    public ResponseEntity<Commerce> creerCommerce(@PathVariable long idFerme, @RequestBody Commerce commerce){
        Commerce c = commerceService.addComerce(commerce);
        if (c != null)
            return ResponseEntity.ok(c);
        else
            return ResponseEntity.notFound().build();

    }

    @GetMapping
    public ResponseEntity<Page<Commerce>> infoCommerce(@PathVariable long idFerme, Pageable pageable){
        Ferme ferme = fermeService.getFerme(idFerme);
        Page<Commerce> page = commerceRepository.findAllByVendeur(ferme, pageable);

        if(page == null)
            return ResponseEntity.notFound().build();
        
        return ResponseEntity.ok(page);
    }
    

    @PutMapping
    public void updateCommerce(@PathVariable long idFerme){
        commerceService.updateCommerce(idFerme);
    } 

    @GetMapping("/eleveurs")
    public ResponseEntity<Page<Commerce>> getInfoVenteNonFini(Pageable pageable){
        Page<Commerce> page = commerceRepository.findAllByAcheteurIsNull(pageable);

        if(page == null)
            return ResponseEntity.notFound().build();

        return ResponseEntity.ok(page);
    }

    /*
    TODO

     @GetMapping("/coop")
    public void getInfoCoop(){}
     */

}
