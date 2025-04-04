package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Clapier;
import com.example.tinyfarm.entity.Ferme;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;


public interface ClapierRepository extends JpaRepository<Clapier, Long> {
    // Page<Clapier> findAll(Pageable pageable);  // Ajout de la pagination
    // Page<Clapier> findAllByFarm(Ferme ferme, Pageable pageable);
    Clapier findByProprietaire(Ferme proprietaire);
    Page<Clapier> findAll(Pageable pageable);
}
