package com.example.tinyfarm.startup;

import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.example.tinyfarm.service.ProduitService;

@Component
@RequiredArgsConstructor
public class DataLoader implements CommandLineRunner {
    private final ProduitService produitService;

    @Override
    public void run(String... args) {
        produitService.populateData();
    }
}
