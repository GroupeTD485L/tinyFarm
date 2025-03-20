package com.example.tinyfarm.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.authgithub.entity.Farm;

public interface FarmRepository extends JpaRepository<Farm, String> {
}
