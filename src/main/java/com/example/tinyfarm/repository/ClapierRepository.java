package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Clapier;

import org.springframework.data.jpa.repository.JpaRepository;


public interface ClapierRepository extends JpaRepository<Clapier, Long> {
    // Page<Clapier> findAll(Pageable pageable);  // Ajout de la pagination
    // Page<Clapier> findAllByFarm(Ferme ferme, Pageable pageable);
}
