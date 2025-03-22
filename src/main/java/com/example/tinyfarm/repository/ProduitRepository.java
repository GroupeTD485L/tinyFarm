package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Produit;

public interface ProduitRepository extends JpaRepository<Produit, String> {
    Page<Produit> findAll(Pageable pageable);  // Ajout de la pagination
    Page<produit> findAllByFarm(Ferme ferme, Pageable pageable)
}
