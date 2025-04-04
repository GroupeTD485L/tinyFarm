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
@RequestMapping("/commerce")
public class CommerceController {
    
    private final CommerceService commerceService;
    private final CommerceRepository commerceRepository;
    private final FermeService fermeService;

    public CommerceController(CompteService compteService, FermeService fermeService, CommerceService commerceService, CommerceRepository commerceRepository){
        this.commerceService = commerceService;
        this.fermeService = fermeService;
        this.commerceRepository = commerceRepository;
    }

    @PostMapping("/admin/addCommerce")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Commerce> creerCommerce(@RequestBody Commerce commerce){
        Commerce c = commerceService.addComerce(commerce);
        if (c != null)
            return ResponseEntity.ok(c);
        else
            return ResponseEntity.notFound().build();

    }

    @PostMapping("/addOffre")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Commerce> creerOffre(Authentication authentication, @RequestBody String nomProduit, @RequestBody int quantite, @RequestBody float prixUnitaire){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        Commerce c = commerceService.addOffre(ferme, nomProduit, quantite, prixUnitaire);
        if (c != null)
            return ResponseEntity.ok(c);
        else
            return ResponseEntity.notFound().build();

    }

    @GetMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Page<Commerce>> infoCommerce(Authentication authentication, Pageable pageable){
        Ferme ferme = fermeService.getOrCreateFermeForUser(authentication.getName());
        if (ferme == null)
            return ResponseEntity.notFound().build();
        Page<Commerce> page = commerceRepository.findAllByVendeur(ferme, pageable);

        if(page == null)
            return ResponseEntity.notFound().build();
        
        return ResponseEntity.ok(page);
    }
    

    @PutMapping
    @PreAuthorize("isAuthenticated()")
    public void updateCommerce(){
        commerceService.updateCommerce();
    } 

    @GetMapping("/eleveurs")
    @PreAuthorize("isAuthenticated()")
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
