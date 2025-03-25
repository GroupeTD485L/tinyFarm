package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.service.FermeService;

@RestController
@RequestMapping("/ferme")
public class FermeController {

    private final FermeService farmService;

    public FermeController(FermeService fermeService) {
        this.fermeService = fermeService;
    }

    @GetMapping
    public Ferme getFerme(Authentication authentication) {
        String username = authentication.getName();
        return fermeService.getOrCreateFermeForUser(username);
    }
}
