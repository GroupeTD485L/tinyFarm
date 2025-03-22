package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Produit;
import  com.example.chicken.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface ProduitRepository extends JpaRepository<Produit, String> {
    Page<Produit> findAll(Pageable pageable);  // Ajout de la pagination
    Page<produit> findAllByFarm(Ferme ferme, Pageable pageable)
}
