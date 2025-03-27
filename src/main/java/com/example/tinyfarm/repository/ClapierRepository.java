package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Clapier;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface ClapierRepository extends JpaRepository<Clapier, Long> {
    // Page<Clapier> findAll(Pageable pageable);  // Ajout de la pagination
    // Page<Clapier> findAllByFarm(Ferme ferme, Pageable pageable);
}
