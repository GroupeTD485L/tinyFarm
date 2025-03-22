package com.example.tinyfarm.repository;

import  com.example.tinyfarm.entity.Transaction;
import  com.example.chicken.entity.Ferme;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


public interface TransactionRepository extends JpaRepository<Transaction, String> {
    Page<Transaction> findAll(Pageable pageable);  // Ajout de la pagination
    Page<Transaction> findAllByFarm(Ferme ferme, Pageable pageable);
}
