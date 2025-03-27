package com.example.tinyfarm.service;

import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.ClassementRepository;
import com.example.tinyfarm.repository.CommerceRepository;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.ProduitRepository;


@Service
public class ClassementService {
    private final ClassementRepository classementRepository;
    private final CommerceRepository commerceRepository;
    private final FermeRepository fermeRepository;
    private final ProduitRepository produitRepository;

    public ClassementService(
            ClassementRepository classementRepository,
            CommerceRepository commerceRepository,
            FermeRepository fermeRepository,
            ProduitRepository produitRepository
        ) {
        this.classementRepository = classementRepository;
        this.commerceRepository = commerceRepository;
        this.fermeRepository = fermeRepository;
        this.produitRepository = produitRepository;
    }

    @Transactional
    public Classement updateScore(Long idClassement) {
        Optional<Classement> classementExisting = classementRepository.findById(idClassement);
        if (!classementExisting.isPresent()) {
            throw new IllegalArgumentException("Le classement d'id " + idClassement + " n'existe pas !");
        }
        Classement classement = classementExisting.get();

        Ferme ferme = classement.getFerme();

        // Quand on fera la coop : retirer 1 pour ne pas compter le joueur coopérative
        long totalJoueur = fermeRepository.count();
        long nbPointOeuf = totalJoueur * 15;
        long nbPointLapin = totalJoueur * 30;
        long nbPointPoule = totalJoueur * 25;
        long nbPointLait = totalJoueur * 20;

        Produit oeuf = produitRepository.findByNom("Oeuf");
        long totalVenteOeuf = commerceRepository.countByProduitAndAcheteurIsNotNull(oeuf);
        long totalVenteOeufJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(oeuf, ferme);
        float scoreOeuf = nbPointOeuf * (totalVenteOeufJoueur/(float)totalVenteOeuf);

        Produit lapin = produitRepository.findByNom("Lapin");
        long totalVenteLapin = commerceRepository.countByProduitAndAcheteurIsNotNull(lapin);
        long totalVenteLapinJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(lapin, ferme);
        float scoreLapin = nbPointLapin * (totalVenteLapinJoueur/(float)totalVenteLapin);

        Produit poule = produitRepository.findByNom("Poule");
        long totalVentePoule = commerceRepository.countByProduitAndAcheteurIsNotNull(poule);
        long totalVentePouleJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(poule, ferme);
        float scorePoule = nbPointPoule * (totalVentePouleJoueur/(float)totalVentePoule);

        Produit lait = produitRepository.findByNom("Lait");
        long totalVenteLait = commerceRepository.countByProduitAndAcheteurIsNotNull(lait);
        long totalVenteLaitJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(lait, ferme);
        float scoreLait = nbPointLait * (totalVenteLaitJoueur/(float)totalVenteLait);

        // TODO: prendre en compte les écus aussi
        classement.setScore(scoreOeuf + scoreLapin + scorePoule + scoreLait);

        return classementRepository.save(classement);
    }

    @Transactional
    public void updateScoreForAllPlayers() {
        Iterable<Classement> classements = classementRepository.findAll();
        for (Classement classement : classements) {
            updateScore(classement.getIdClassement());
        }
    }

    @Transactional
    public Page<Classement> getAllClassement(Pageable pageable) {
        return classementRepository.findAll(pageable);
    }

    @Transactional
    public Classement getScore(Long idClassement) {
        Optional<Classement> existingClassement = classementRepository.findById(idClassement);
        if (existingClassement.isPresent()) {
            return existingClassement.get();
        }
        // Décommenter dans le cas où il fallait effectivement trouver le score
        /*
        Optional<Ferme> existingFerme = fermeRepository.findById(idFerme);
        if (existingFerme.isPresent()) {
            Ferme ferme = existingFerme.get();
            Classement classement = new Classement();
            classement.setFerme(ferme);
            classement.setScore(0);
            return classementRepository.save(classement);
        }*/
        else {
            throw new IllegalArgumentException("Le classement " + idClassement + " n'existe pas !");
        }
    }
}