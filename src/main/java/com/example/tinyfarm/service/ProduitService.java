package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.Produit;
import com.example.tinyfarm.repository.ProduitRepository;

import java.util.Optional;
import java.util.ArrayList;
import java.util.List;

@Service
public class ProduitService {
    private final ProduitRepository produitRepository;

    public ProduitService(ProduitRepository produitRepository) {
        this.produitRepository = produitRepository;
    }

    @Transactional
    public Produit getProduit(String nomProduit) {
        Optional<Produit> existingProduit = produitRepository.findByNom(nomProduit);
        if (!existingProduit.isPresent()) {
            throw new IllegalArgumentException("Il n'y a pas de produit nommé " + nomProduit + " !");
        }
        return existingProduit.get();
    }

    @Transactional
    public void populateData() {
        List<String> nomsProduits = new ArrayList<>(List.of(
            "Seau d'eau",
            "Botte de foin",
            "Seringue",
            "Savon",
            "Oeuf",
            "Lait",
            "Graine"
            // TODO : Rajouter les objets si besoin
        ));

        for (String nomProduit : nomsProduits) {
            Produit produit = new Produit(nomProduit);
            produitRepository.save(produit);
        }
    }
}
