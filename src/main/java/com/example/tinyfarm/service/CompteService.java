package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.CompteRepository;

import java.util.Optional;

@Service
public class CompteService {
    
    private final CompteRepository compteRepository;

    public CompteService(CompteRepository compteRepository) {
        this.compteRepository = compteRepository;
    }

    @Transactional
    public Compte getCompte(Long idCompte) {
        Optional<Compte> existingCompte = compteRepository.findById(idCompte);
        if (existingCompte.isPresent()) {
            return existingCompte.get();
        } else {
            throw new IllegalArgumentException("Le compte d'id " + idCompte + " n'existe pas !");
        }
    }

    @Transactional
    public Compte getCompte(String pseudo) {
        Optional<Compte> existingCompte = compteRepository.findByPseudo(pseudo);
        if (existingCompte.isPresent()) {
            return existingCompte.get();
        } else {
            throw new IllegalArgumentException("Le compte " + pseudo + " n'existe pas !");
        }
    }

    @Transactional
    public Compte updateCompte(Long idCompte) {
        Optional<Compte> existingCompte = compteRepository.findById(idCompte);

        if (existingCompte.isPresent()) {
            Compte compte = existingCompte.get();
            compte.setDerniereConnexion(LocalDateTime.now());
            return compteRepository.save(compte);
        } else {
            throw new IllegalArgumentException("Le compte d'id " + idCompte + " n'existe pas !");
        }
    }

    @Transactional
    public Compte updateCompte(String pseudo) {
        Optional<Compte> existingCompte = compteRepository.findByPseudo(pseudo);

        if (existingCompte.isPresent()) {
            return updateCompte(existingCompte.get().getIdCompte());
        } else {
            throw new IllegalArgumentException("Le compte " + pseudo + " n'existe pas !");
        }
    }

    @Transactional
    public void deleteCompte(Long idCompte) {
        Optional<Compte> existingCompte = compteRepository.findById(idCompte);

        if (existingCompte.isPresent()) {
            compteRepository.delete(existingCompte.get());
        } else {
            throw new IllegalArgumentException("Le compte d'id " + idCompte + " n'existe pas !");
        }
    }

    @Transactional
    public void deleteCompte(String pseudo) {
        Optional<Compte> existingCompte = compteRepository.findByPseudo(pseudo);

        if (existingCompte.isPresent()) {
            compteRepository.delete(existingCompte.get());
        } else {
            throw new IllegalArgumentException("Le compte " + pseudo + " n'existe pas !");
        }
    }
}
