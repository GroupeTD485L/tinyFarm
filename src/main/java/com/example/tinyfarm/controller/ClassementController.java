package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;

import  com.example.tinyfarm.entity.Classement;
import  com.example.tinyfarm.service.ClassementService;

@RestController
@RequestMapping("/classements") // URL
public class ClassementController {

    private final ClassementService classementService;

    public ClassementController(ClassementService classementService){
        this.classementService = classementService;
    }

    // Obtenir les infos du classement
    @PreAuthorize("isAuthenticated()")
    @GetMapping
    public ResponseEntity<Page<Classement>> getClassement(@PageableDefault Pageable pageable){
        Page<Classement> classement = classementService.getAllClassement(pageable); // Récupére les infos du classement
        if(classement != null) {
            return ResponseEntity.ok(classement); // On renvoie les infos du classement
        } else {
            // Si le classement est inexistant
             return ResponseEntity.notFound().build();
        }
    }
}