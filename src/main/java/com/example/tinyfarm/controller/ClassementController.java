/*package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import  com.example.tinyfarm.entity.Classement;
import  com.example.tinyfarm.service.ClassementService;

@RestController
// @PreAuthorize("isAuthenticated()")
@RequestMapping("/classements")
public class ClassementController {
    
    private final ClassementService classementService;

    public ClassementController(ClassementService classementService){
        this.classementService = classementService;
    }

    @GetMapping
    public Classement infosClassement(){}

}
*/