package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.*;

import java.util.Optional;
import java.time.LocalDateTime;
import java.util.ArrayList;

@Service
public class FermeService {

    private final ClassementRepository classementRepository;

    private final FermeRepository fermeRepository;
    private final VacheRepository vacheRepository;
    private final ClapierRepository clapierRepository;
    private final PouleRepository pouleRepository;
    private final CompteRepository compteRepository;

    public FermeService(
            FermeRepository fermeRepository,
            VacheRepository vacheRepository,
            ClapierRepository clapierRepository,
            PouleRepository pouleRepository,
            CompteRepository compteRepository,
            ClassementRepository classementRepository) {
        this.fermeRepository = fermeRepository;
        this.vacheRepository = vacheRepository;
        this.clapierRepository = clapierRepository;
        this.pouleRepository = pouleRepository;
        this.compteRepository = compteRepository;
        this.classementRepository = classementRepository;
    }

    @Transactional
    public Ferme getOrCreateFermeForUser(String pseudo) {
        Optional<Ferme> existingFerme = fermeRepository.findByComptePseudo(pseudo);
        if (existingFerme.isPresent()) {
            Ferme ferme = existingFerme.get();
            Compte compte = ferme.getCompte();
            compte.setDerniereConnexion(LocalDateTime.now());
            compteRepository.save(compte);
            return existingFerme.get();
        }

        Ferme ferme = new Ferme("Ferme de " + pseudo);

        // Création du compte
        Compte compte = new Compte(pseudo, ferme);
        compte.setDerniereConnexion(LocalDateTime.now());
        ferme.setCompte(compte);
        compte.setIdFerme(ferme);
        compteRepository.save(compte);
        
        // Création des poules
        ArrayList<Poule> poules = new ArrayList<Poule>();
        //initialisation des 3 poules
        Poule poule = new Poule('M', 2.5, 5);
        poule.setProprietaire(ferme);
        poules.add(poule);

        poule = new Poule('F', 2.5, 5);
        poule.setProprietaire(ferme);
        poules.add(poule);
        
        poule = new Poule('F', 2.5, 5);
        poule.setProprietaire(ferme);
        poules.add(poule);
        ferme.setPoules(poules);
        pouleRepository.saveAll(poules);

        // Création des vaches
        Vache vache = new Vache();
        ferme.setVache(vache);
        vache.setProprietaire(ferme);
        vacheRepository.save(vache);

        // Création du clapier
        Clapier clapier = new Clapier();
        ferme.setClapier(clapier);
        clapier.setProprietaire(ferme);
        clapierRepository.save(clapier);
        
        // Création du classement
        Classement classement = new Classement();
        classement.setFerme(ferme);
        ferme.setClassement(classement);
        classementRepository.save(classement);
        return fermeRepository.save(ferme);
    }

    @Transactional
    public Ferme getFerme(Long idFerme) {
        Optional<Ferme> existingFerme = fermeRepository.findById(idFerme);
        if (existingFerme.isPresent()) {
            return existingFerme.get();
        } else {
            throw new IllegalArgumentException("La ferme " + idFerme + " n'existe pas !");
        }
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
