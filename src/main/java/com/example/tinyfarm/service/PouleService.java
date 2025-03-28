package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.Duration;

import com.example.tinyfarm.entity.*;
import com.example.tinyfarm.repository.PouleRepository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;
import java.util.Random;

@Service
public class PouleService {

    private final PouleRepository pouleRepository;

    public PouleService(PouleRepository pouleRepository) {
        this.pouleRepository = pouleRepository;
    }

    @Transactional
    public Page<Poule> getAllPoules(Pageable pageable) {
        return pouleRepository.findAll(pageable);
    }

    @Transactional
    public Page<Poule> getPoulesByProprietaireAndSexe(Ferme ferme, char sexe, Pageable pageable) {
        return pouleRepository.findAllByProprietaireAndSexe(ferme, sexe, pageable);
    }

    @Transactional
    public Page<Poule> getPoulesBySexe(char sexe, Pageable pageable) {
        return pouleRepository.findAllBySexe(sexe, pageable);
    }

    @Transactional
    public Optional<Poule> getPouleById(Long id) {
        return pouleRepository.findById(id);
    }

    @Transactional
    public Poule addPoule(Poule poule) {
        return pouleRepository.save(poule);
    }

    @Transactional
    public void deletePoule(Long id) {
        pouleRepository.deleteById(id);
    }

    @Transactional
    public void updatePoule(Long id) {
        Optional<Poule> existingPoule = pouleRepository.findById(id);
        Poule poule = existingPoule.get();
        long differenceInDays = Duration.between(poule.getDernierRepas(), LocalDateTime.now()).toDays();
        if ( differenceInDays == 1) {
            poule.setPoids(poule.getPoids()-0.2);
        } else if ( differenceInDays == 2) {
            poule.setPoids(poule.getPoids()-0.5);
        } else if ( differenceInDays == 3) {
            poule.setPoids(poule.getPoids()-1);
        } else if (differenceInDays >= 4) {
            pouleRepository.deleteById(id); // La poule meurt, on la supprime
        }
        if (Duration.between(poule.getMaladeDepuis(), LocalDateTime.now()).toDays() >= 4) {
            pouleRepository.deleteById(id); // La poule meurt, on la supprime
        }
        if (poule.getAge()>=5 && poule.getPoids()>= 2.5) {
            Random random = new Random();
            poule.setSexe(random.nextBoolean() ? 'M' : 'F');
        }
    
    }
}