package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Clapier;

public interface ClapierRepository extends JpaRepository<Clapier, String> {
    Page<Clapier> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Clapier> findAllByFarm(Ferme ferme, Pageable pageable);
}
