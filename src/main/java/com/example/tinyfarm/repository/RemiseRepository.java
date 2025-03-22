package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Remise;

public interface RemiseRepository extends JpaRepository<Remise, String> {
    Page<Remise> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Remise> findAllByFarm(Ferme ferme, Pageable pageable);
}
