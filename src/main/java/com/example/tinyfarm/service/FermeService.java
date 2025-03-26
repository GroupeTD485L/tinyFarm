package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.FermeRepository;

import java.util.Optional;

@Service
public class FermeService {

    private final FermeRepository fermeRepository;

    public FermeService(FermeRepository fermeRepository) {
        this.fermeRepository = fermeRepository;
    }

    @Transactional
    public Ferme getOrCreateFermeForUser(String pseudo) {
        Optional<Ferme> existingFerme = fermeRepository.findByComptePseudo(pseudo);
        if (existingFerme.isPresent()) {
            return existingFerme.get();
        }

        Ferme ferme = new Ferme("Ferme de " + pseudo);
        Compte compte = new Compte(pseudo, ferme);
        ferme.setCompte(compte);

        return fermeRepository.save(ferme);
    }

    @Transactional
    public Ferme updateFerme(String pseudo) {
        Optional<Ferme> existingFerme = fermeRepository.findByComptePseudo(pseudo);
        if (existingFerme.isPresent()) {
            Ferme ferme = existingFerme.get();
            // TODO: mettre à jour les différents attributs
            ferme.setAchatRestant(12);
            return fermeRepository.save(ferme);
        }
        throw new IllegalArgumentException("Le pseudo " + pseudo + " n'existe pas !");
    }

    @Transactional
    public void deleteFerme(String pseudo) {
        Optional<Ferme> existingFerme = fermeRepository.findByComptePseudo(pseudo);
        if (existingFerme.isPresent()) {
            fermeRepository.delete(existingFerme.get());
        } else {
            throw new IllegalArgumentException("Le pseudo " + pseudo + " n'existe pas !");
        }
    }
    /*
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
    */
}
