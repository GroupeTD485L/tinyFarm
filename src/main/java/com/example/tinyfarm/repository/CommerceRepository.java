package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.*;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface CommerceRepository extends JpaRepository<Commerce, Long> {
    Page<Commerce> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Commerce> findAllByVendeur(Ferme ferme, Pageable pageable);
    long countByProduitAndAcheteurIsNotNull(Produit produit);
    long countByProduitAndVendeurAndAcheteurIsNotNull(Produit produit, Ferme vendeur);
}
