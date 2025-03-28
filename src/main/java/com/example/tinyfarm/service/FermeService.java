package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.RemiseRepository;
import com.example.tinyfarm.repository.VacheRepository;
import com.example.tinyfarm.repository.ClapierRepository;
import com.example.tinyfarm.repository.PouleRepository;
import com.example.tinyfarm.repository.CompteRepository;

import java.util.Optional;
import java.util.ArrayList;

@Service
public class FermeService {

    private final FermeRepository fermeRepository;
    private final VacheRepository vacheRepository;
    private final ClapierRepository clapierRepository;
    private final PouleRepository pouleRepository;
    private final CompteRepository compteRepository;
    private final RemiseRepository remiseRepository;

    public FermeService(
            FermeRepository fermeRepository,
            VacheRepository vacheRepository,
            ClapierRepository clapierRepository,
            PouleRepository pouleRepository,
            CompteRepository compteRepository,
            RemiseRepository remiseRepository
        ) {
        this.fermeRepository = fermeRepository;
        this.vacheRepository = vacheRepository;
        this.clapierRepository = clapierRepository;
        this.pouleRepository = pouleRepository;
        this.compteRepository = compteRepository;
        this.remiseRepository = remiseRepository;
    }

    @Transactional
    public Ferme getOrCreateFermeForUser(String pseudo) {
        Optional<Ferme> existingFerme = fermeRepository.findByComptePseudo(pseudo);
        if (existingFerme.isPresent()) {
            return existingFerme.get();
        }

        Ferme ferme = new Ferme("Ferme de " + pseudo);
        Vache vache = new Vache();
        Clapier clapier = new Clapier();
        ArrayList<Poule> poules = new ArrayList<Poule>();
        Compte compte = new Compte(pseudo, ferme);
        Remise remise = new Remise();
        
        //initialisation des 3 poules
        poules.add(new Poule('M', 2.5, 5));
        poules.add(new Poule('F', 2.5, 5));
        poules.add(new Poule('F', 2.5, 5));

        ferme.setCompte(compte);
        compteRepository.save(compte);
        ferme.setVache(vache);
        vacheRepository.save(vache);
        ferme.setClapier(clapier);
        clapierRepository.save(clapier);
        ferme.setPoules(poules);
        pouleRepository.saveAll(poules);
        ferme.setRemise(remise);
        remiseRepository.save(remise);

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
