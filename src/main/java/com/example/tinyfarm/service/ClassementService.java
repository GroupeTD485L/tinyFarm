package com.example.tinyfarm.service;

import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.PageRequest;

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

        Optional<Produit> existOeuf =  produitRepository.findByNom("Oeuf");
        if (!existOeuf.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit oeuf = existOeuf.get();
        long totalVenteOeuf = commerceRepository.countByProduitAndAcheteurIsNotNull(oeuf);
        long totalVenteOeufJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(oeuf, ferme);
        float scoreOeuf = nbPointOeuf * (totalVenteOeufJoueur/(float)totalVenteOeuf);

        Optional<Produit> existLapin =  produitRepository.findByNom("Lapin");
        if (!existLapin.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit lapin = existLapin.get();
        long totalVenteLapin = commerceRepository.countByProduitAndAcheteurIsNotNull(lapin);
        long totalVenteLapinJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(lapin, ferme);
        float scoreLapin = nbPointLapin * (totalVenteLapinJoueur/(float)totalVenteLapin);

        Optional<Produit> existPoule =  produitRepository.findByNom("Poule");
        if (!existPoule.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit poule = existPoule.get();
        long totalVentePoule = commerceRepository.countByProduitAndAcheteurIsNotNull(poule);
        long totalVentePouleJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(poule, ferme);
        float scorePoule = nbPointPoule * (totalVentePouleJoueur/(float)totalVentePoule);

        Optional<Produit> existLait =  produitRepository.findByNom("Lait");
        if (!existLait.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit lait = existLait.get();
        long totalVenteLait = commerceRepository.countByProduitAndAcheteurIsNotNull(lait);
        long totalVenteLaitJoueur = commerceRepository.countByProduitAndVendeurAndAcheteurIsNotNull(lait, ferme);
        float scoreLait = nbPointLait * (totalVenteLaitJoueur/(float)totalVenteLait);

        // TODO: prendre en compte les écus aussi
        classement.setScore(scoreOeuf + scoreLapin + scorePoule + scoreLait);

        return classementRepository.save(classement);
    }

    @Transactional
    public void updateScoreForAllPlayers() {
        int iPage = 0;
        Page<Classement> classements;
        do {
            classements = classementRepository.findAll(PageRequest.of(iPage, 20));
            for (Classement classement : classements) {
                updateScore(classement.getIdClassement());
            }
            iPage++;
        } while (classements.hasNext());
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