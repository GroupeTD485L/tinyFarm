package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import  com.example.tinyfarm.entity.Transaction;

public interface TransactionRepository extends JpaRepository<Transaction, String> {
}
