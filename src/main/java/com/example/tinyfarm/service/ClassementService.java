package com.example.tinyfarm.service;

import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.ClassementRepository;
import com.example.tinyfarm.repository.CommerceRepository;
// import com.example.tinyfarm.repository.FermeRepository;

@Service
public class ClassementService {
    private final ClassementRepository classementRepository;
    // private final FermeRepository fermeRepository;

    public ClassementService(
            ClassementRepository classementRepository
            // FermeRepository fermeRepository
        ) {
        this.classementRepository = classementRepository;
        // this.fermeRepository = fermeRepository;
    }

    @Transactional
    public Classement getScore(Long idFerme) {
        Optional<Classement> existingClassement = classementRepository.findById(idFerme);
        if (existingClassement.isPresent()) {
            return existingClassement.get();
        }
        // Décommenter dans le cas où il fallait effectivement trouver le score
        /*
        Optional<Ferme> existingFerme = fermeRepository.findById(idFerme);
        if (existingFerme.isPresent()) {
            Ferme ferme = existingFerme.get();
            Classement classement = new Classement();
            classement.setFerme(ferme);
            classement.setScore(0);
            return classementRepository.save(classement);
        }*/
        else {
            throw new IllegalArgumentException("La ferme " + idFerme + " n'existe pas !");
        }
    }
}