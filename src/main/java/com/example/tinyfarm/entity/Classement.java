package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "classement")
public class Classement{
    @Id
    @OneToOne
    @JoinColumn(name="idFerme", nullable = false)
    private Ferme idFerme;

    private float score;

    public Classement(){}

    public Classement(float score){
        this.score = score;
    }
}
