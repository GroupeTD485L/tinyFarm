package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Produit;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface ProduitRepository extends JpaRepository<Produit, Long> {
    Page<Produit> findAll(Pageable pageable);  // Ajout de la pagination
    Produit findById(Long id);
    // Page<Produit> findAllByFarm(Ferme ferme, Pageable pageable);
    Produit findByNom(String nom); // trouve un produit avec son nom 
}
