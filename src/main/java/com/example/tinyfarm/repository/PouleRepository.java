package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Poule;
import  com.example.tinyfarm.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface PouleRepository extends JpaRepository<Poule, Long> {
    Page<Poule> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Poule> findAllByProprietaire(Ferme ferme, Pageable pageable);
    Optional<Poule> findById(Long id);
}
