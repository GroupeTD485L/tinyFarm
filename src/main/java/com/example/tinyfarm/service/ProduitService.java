package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.Produit;
import com.example.tinyfarm.repository.ProduitRepository;

import java.util.Optional;

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
}
