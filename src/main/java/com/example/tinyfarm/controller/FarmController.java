package com.example.tinyfarm.controller;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import com.example.authgithub.entity.Farm;
import com.example.authgithub.service.FarmService;

@RestController
@RequestMapping("/farm")
public class FarmController {

    private final FarmService farmService;

    public FarmController(FarmService farmService) {
        this.farmService = farmService;
    }

    @GetMapping
    public Farm getFarm(Authentication authentication) {
        String username = authentication.getName();
        return farmService.getOrCreateFarmForUser(username);
    }
}
