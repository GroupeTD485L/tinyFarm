package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import  com.example.tinyfarm.entity.Ferme;
import  com.example.tinyfarm.repository.FermeRepository;

import java.util.Optional;

@Service
public class FermeService {

    private final FermeRepository fermeRepository;

    public FermeService(FermeRepository fermeRepository) {
        this.fermeRepository = fermeRepository;
    }

    @Transactional
    public Ferme getOrCreateFermeForUser(String username) {
        // Vérifier si la ferme existe déjà
        Optional<Ferme> existingFerme = fermeRepository.findById(username);
        if (existingFerme.isPresent()) {
            return existingFerme.get(); // Retourner la ferme existante
        }

        // Sinon, créer une nouvelle ferme
        Ferme newFerme = new Ferme("My Farm");
        return fermeRepository.save(newFerme);
    }
}
