package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Remise;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface RemiseRepository extends JpaRepository<Remise, Long> {
    Page<Remise> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Remise> findAllByProprietaire(Ferme ferme, Pageable pageable);
}
